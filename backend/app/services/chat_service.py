from openai import AsyncOpenAI
from app.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.supabase_service import SupabaseService
from typing import List, Dict
import json

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class ChatService:
    @staticmethod
    async def summarize_old_messages(messages: List[Dict]) -> str:
        """Summarize older parts of conversation"""
        text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo", # Cheaper model for summarization
                messages=[
                    {"role": "system", "content": "Summarize the key points of this conversation concisely."},
                    {"role": "user", "content": text}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error summarizing messages: {e}")
            return "Previous conversation summary unavailable."

    @staticmethod
    async def generate_response(
        query: str,
        session_id: str,
        language: str = "en",
        conversation_history: List[Dict] = None
    ) -> Dict:
        """Generate AI response using RAG with Memory"""
        
        # 1. Load recent history if not provided
        if conversation_history is None:
            conversation_history = SupabaseService.get_chat_history(session_id, limit=20)
        
        # 2. Handle long history with summarization
        system_context_messages = []
        recent_messages = conversation_history
        
        if len(conversation_history) > 10:
            # Summarize everything except last 5 messages
            to_summarize = conversation_history[:-5]
            recent_messages = conversation_history[-5:]
            
            summary = await ChatService.summarize_old_messages(to_summarize)
            system_context_messages.append({
                "role": "system", 
                "content": f"Previous conversation summary: {summary}"
            })
            
        # 3. Retrieve relevant chunks from vector database
        relevant_chunks = await EmbeddingService.search_similar_chunks(
            query, 
            session_id, 
            limit=settings.MAX_CHUNKS_RETRIEVAL
        )
        
        # 4. Build context from retrieved chunks
        context_text = "\n\n".join([
            f"[From {chunk['filename']}]:\n{chunk['text']}"
            for chunk in relevant_chunks
        ])
        
        if not relevant_chunks and not conversation_history:
             # If no docs and no history, guide user
             return {
                "response": "I don't see any documents uploaded yet. Please upload a document so I can answer your questions.",
                "sources": [],
                "chunks_used": 0
            }

        # 5. System prompt
        system_prompt = f"""You are an intelligent document assistant. Answer questions based on the provided context and conversation history.

Instructions:
1. Use the Context from documents to answer the user's question.
2. Use the Conversation Summary and History to maintain continuity.
3. Always cite sources with [filename] references when using document context.
4. If the answer isn't in the context, say so clearly, unless it's a general conversational follow-up.
5. Respond in {language} language.

Context from documents:
{context_text}
"""
        
        # 6. Build final message list for OpenAI
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(system_context_messages) # Add summary if any
        
        # Add recent history (excluding system messages if we want to be strict, but usually fine)
        for msg in recent_messages:
            # Ensure we only send role/content to OpenAI
            messages.append({"role": msg["role"], "content": msg["content"]})
            
        messages.append({"role": "user", "content": query})
        
        # 7. Generate response
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        
        # Extract sources
        sources = list(set([chunk["filename"] for chunk in relevant_chunks]))
        
        # 8. Save messages to Supabase (Async/Background ideally, but direct for now)
        SupabaseService.add_message(session_id, "user", query, language)
        SupabaseService.add_message(session_id, "assistant", answer, language, sources)
        
        return {
            "response": answer,
            "sources": sources,
            "chunks_used": len(relevant_chunks),
            "relevant_chunks": relevant_chunks[:3]
        }
