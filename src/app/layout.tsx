import type { Metadata } from "next";
import Script from "next/script";
import "./globals.css";
export const metadata: Metadata = {
  title: "Docly-AI ChatBot",
  description: "Chat with documents",
  openGraph: {
    title: "Docly-AI ChatBot",
    description: "Chat with documents",
    url: "",
    siteName: "Docly-AI ChatBot",
    type: "website",
  },
  icons: {
    icon: "/favicon.png",
  },
};
export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" data-oid="b1jifow">
      <body className="antialiased" data-oid="hqec2:a">
        {children}

        <Script
          src="https://cdn.jsdelivr.net/gh/onlook-dev/onlook@d3887f2/apps/web/client/public/onlook-preload-script.js"
          strategy="afterInteractive"
          type="module"
          id="onlook-preload-script"
          data-oid="_g:405r"
        ></Script>
      </body>
    </html>
  );
}
