import { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { ChatbotButton } from '@/components/ChatbotButton';

interface LayoutProps {
    children: ReactNode;
}

const Header = () => (
  <header className="bg-white shadow-sm border-b">
    <div className="container mx-auto px-4 py-4">
      <Link to="/" className="flex items-center gap-2 text-xl font-bold">
        <img
          src="/favicon.ico"
          alt="AdmitTree logo"
          className="h-10 w-auto"
        />
        AdmitTree
      </Link>
    </div>
  </header>
);

const Footer = () => (
    <footer className="bg-gray-50 border-t mt-auto">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-gray-600">
            © 2026 AdmitTree. All rights reserved.
        </div>
    </footer>
);

export const Layout = ({ children }: LayoutProps) => (
    <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
        <ChatbotButton />
    </div>
);
