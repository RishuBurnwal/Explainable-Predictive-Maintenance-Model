import React, { useState, useEffect } from "react";
import Navigation from "@/components/Navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { BookOpen, FileText, Scale, Lightbulb, Home, Download, Book, HelpCircle, Settings, Rocket, Network, Zap } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { tomorrow } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Link } from "react-router-dom";

interface DocumentSection {
  id: string;
  title: string;
  icon: React.ElementType;
  description: string;
  file: string;
}

const Documentation = () => {
  const [activeSection, setActiveSection] = useState("overview");
  const [documentContent, setDocumentContent] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  const documentSections: DocumentSection[] = [
    {
      id: "overview",
      title: "README",
      icon: BookOpen,
      description: "Project overview and getting started guide",
      file: "README.md"
    },
    {
      id: "quickstart",
      title: "Quick Start",
      icon: Zap,
      description: "Fast setup guide to get running in minutes",
      file: "QUICK_START.md"
    },
    {
      id: "setup",
      title: "Project Setup",
      icon: Settings,
      description: "Installation guide and project structure",
      file: "PROJECT_SETUP.md"
    },
    {
      id: "summary",
      title: "Project Summary",
      icon: Book,
      description: "Complete system documentation and features",
      file: "PROJECT_SUMMARY.md"
    },
    {
      id: "architecture",
      title: "Architecture",
      icon: Network,
      description: "System architecture and component design",
      file: "ARCHITECTURE.md"
    },
    {
      id: "faq",
      title: "FAQ",
      icon: HelpCircle,
      description: "Frequently asked questions and troubleshooting",
      file: "FAQ.md"
    },
    {
      id: "deployment",
      title: "Deployment",
      icon: Rocket,
      description: "Production deployment guide and best practices",
      file: "DEPLOYMENT.md"
    },
    {
      id: "license",
      title: "License",
      icon: Scale,
      description: "MIT License and usage terms",
      file: "LICENSE.md"
    }
  ];

  useEffect(() => {
    const loadDocuments = async () => {
      setLoading(true);
      const contents: Record<string, string> = {};
      
      for (const section of documentSections) {
        try {
          const response = await fetch(`/docs/${section.file}`);
          if (response.ok) {
            contents[section.id] = await response.text();
          } else {
            contents[section.id] = `# ${section.title}\n\nDocument not found. Please check if the file exists.`;
          }
        } catch (error) {
          console.error(`Error loading ${section.file}:`, error);
          contents[section.id] = `# ${section.title}\n\nError loading document. Please try again later.`;
        }
      }
      
      setDocumentContent(contents);
      setLoading(false);
    };

    loadDocuments();
  }, []);

  const renderMarkdown = (content: string) => (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        h1: ({ children }) => (
          <h1 className="text-2xl md:text-4xl font-bold mb-6 text-foreground border-b border-border pb-4 break-words">
            {children}
          </h1>
        ),
        h2: ({ children }) => (
          <h2 className="text-xl md:text-3xl font-semibold mb-4 mt-8 text-foreground break-words">
            {children}
          </h2>
        ),
        h3: ({ children }) => (
          <h3 className="text-lg md:text-2xl font-semibold mb-3 mt-6 text-foreground break-words">
            {children}
          </h3>
        ),
        h4: ({ children }) => (
          <h4 className="text-base md:text-xl font-semibold mb-2 mt-4 text-foreground break-words">
            {children}
          </h4>
        ),
        p: ({ children }) => (
          <p className="mb-4 text-muted-foreground leading-relaxed break-words">
            {children}
          </p>
        ),
        ul: ({ children }) => (
          <ul className="mb-4 ml-6 list-disc text-muted-foreground">
            {children}
          </ul>
        ),
        ol: ({ children }) => (
          <ol className="mb-4 ml-6 list-decimal text-muted-foreground">
            {children}
          </ol>
        ),
        li: ({ children }) => (
          <li className="mb-1">
            {children}
          </li>
        ),
        blockquote: ({ children }) => (
          <blockquote className="border-l-4 border-primary pl-4 italic mb-4 text-muted-foreground">
            {children}
          </blockquote>
        ),
        table: ({ children }) => (
          <div className="overflow-x-auto mb-4">
            <table className="min-w-full border border-border rounded-lg">
              {children}
            </table>
          </div>
        ),
        th: ({ children }) => (
          <th className="border border-border px-4 py-2 bg-muted font-semibold text-left">
            {children}
          </th>
        ),
        td: ({ children }) => (
          <td className="border border-border px-4 py-2 text-muted-foreground">
            {children}
          </td>
        ),
        code: ({ node, inline, className, children, ...props }) => {
          const match = /language-(\w+)/.exec(className || '');
          return !inline && match ? (
            <SyntaxHighlighter
              style={tomorrow}
              language={match[1]}
              PreTag="div"
              {...props}
            >
              {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
          ) : (
            <code className={className} {...props}>
              {children}
            </code>
          );
        }
      }}
    >
      {content}
    </ReactMarkdown>
  );

  return (
    <div className="min-h-screen bg-background">
      {/* GitHub-style Header */}
      <div className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button asChild variant="ghost" size="sm">
                <Link to="/" className="flex items-center gap-2">
                  <Home className="h-4 w-4" />
                  Back to Dashboard
                </Link>
              </Button>
              <div className="h-4 w-px bg-border"></div>
              <div className="flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-primary" />
                <h1 className="text-lg font-semibold">Documentation</h1>
              </div>
            </div>
            <Button size="sm" variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Download
            </Button>
          </div>
        </div>
      </div>

      {/* GitHub-style Tab Navigation */}
      <div className="border-b border-border bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="flex gap-0 overflow-x-auto">
            {documentSections.map((section) => {
              const IconComponent = section.icon;
              return (
                <Button
                  key={section.id}
                  variant="ghost"
                  size="sm"
                  className={`rounded-none border-b-2 transition-all duration-200 px-4 py-3 min-w-fit ${
                    activeSection === section.id
                      ? 'border-primary text-primary bg-background'
                      : 'border-transparent hover:border-border hover:text-foreground'
                  }`}
                  onClick={() => setActiveSection(section.id)}
                >
                  <IconComponent className="h-4 w-4 mr-2" />
                  {section.title}
                </Button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Documentation Content */}
      <div className="container mx-auto px-4 py-6">
        {loading ? (
          <div className="flex items-center justify-center py-16">
            <div className="flex items-center gap-2 text-muted-foreground">
              <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
              Loading documentation...
            </div>
          </div>
        ) : (
          <div className="max-w-none">
            <div className="bg-background border border-border rounded-lg overflow-hidden">
              <div className="p-6 border-b border-border bg-muted/30">
                <div className="flex items-center gap-2">
                  {documentSections.find(s => s.id === activeSection)?.icon && (
                    React.createElement(documentSections.find(s => s.id === activeSection)!.icon, {
                      className: "h-5 w-5 text-primary"
                    })
                  )}
                  <h2 className="text-xl font-semibold">
                    {documentSections.find(s => s.id === activeSection)?.title}
                  </h2>
                </div>
                <p className="text-sm text-muted-foreground mt-1">
                  {documentSections.find(s => s.id === activeSection)?.description}
                </p>
              </div>
              <div className="p-6">
                <div className="prose prose-gray dark:prose-invert max-w-none">
                  {documentContent[activeSection] && renderMarkdown(documentContent[activeSection])}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Quick Links Footer */}
      <section className="border-t border-border py-12 mt-16">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-6">
            <h3 className="text-2xl font-bold">Quick Links</h3>
            <div className="grid md:grid-cols-3 gap-4 max-w-4xl mx-auto">
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader className="text-center">
                  <Lightbulb className="h-8 w-8 text-primary mx-auto mb-2" />
                  <CardTitle className="text-lg">Getting Started</CardTitle>
                  <CardDescription>
                    Quick setup guide for frontend and backend
                  </CardDescription>
                </CardHeader>
              </Card>
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader className="text-center">
                  <FileText className="h-8 w-8 text-primary mx-auto mb-2" />
                  <CardTitle className="text-lg">API Reference</CardTitle>
                  <CardDescription>
                    Complete API endpoints and usage examples
                  </CardDescription>
                </CardHeader>
              </Card>
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader className="text-center">
                  <BookOpen className="h-8 w-8 text-primary mx-auto mb-2" />
                  <CardTitle className="text-lg">System Architecture</CardTitle>
                  <CardDescription>
                    Technical details and implementation guide
                  </CardDescription>
                </CardHeader>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Documentation;