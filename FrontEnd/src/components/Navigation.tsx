import { Activity, Menu, X, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const scrollToSection = (id: string) => {
    // If we're not on the home page, navigate there first
    if (location.pathname !== '/') {
      navigate('/');
      // Wait for navigation to complete, then scroll
      setTimeout(() => {
        scrollToSectionOnPage(id);
      }, 100);
    } else {
      scrollToSectionOnPage(id);
    }
    setIsMenuOpen(false);
  };

  const scrollToSectionOnPage = (id: string) => {
    // Handle special cases for navigation
    if (id === 'home') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (id === 'dashboard') {
      // Scroll to the dashboard section (status cards)
      const element = document.querySelector('.animate-fade-in');
      element?.scrollIntoView({ behavior: "smooth" });
    } else {
      // Regular scroll to section by ID
      const element = document.getElementById(id);
      element?.scrollIntoView({ behavior: "smooth" });
    }
  };

  const navItems = [
    { name: "Home", id: "home" },
    { name: "Dashboard", id: "dashboard" },
    { name: "Visualizations", id: "visualizations" },
    { name: "Alerts", id: "alerts" },
    { name: "About", id: "about" },
    { 
      name: "Documentation", 
      id: "documentation",
      path: "/documentation"
    }
  ];

  return (
    <nav className="sticky top-0 z-50 glass-card border-b border-border backdrop-blur-xl">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-2 group cursor-pointer">
            <div className="relative">
              <Activity className="h-6 w-6 text-primary group-hover:rotate-12 transition-transform duration-300" />
              <div className="absolute inset-0 h-6 w-6 bg-primary/20 rounded-full blur-sm group-hover:blur-md transition-all duration-300"></div>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-foreground to-primary bg-clip-text text-transparent">
              PredictMaint AI
            </span>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {navItems.map((item) => (
              item.path ? (
                <Link
                  key={item.name}
                  to={item.path}
                  className="relative text-sm font-medium text-muted-foreground hover:text-foreground transition-all duration-300 group flex items-center gap-1"
                >
                  {item.name === 'Documentation' && <BookOpen className="h-4 w-4" />}
                  <span className="relative z-10">{item.name}</span>
                  <div className="absolute inset-0 bg-primary/10 rounded-lg scale-0 group-hover:scale-100 transition-transform duration-300 -z-0"></div>
                  <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary group-hover:w-full transition-all duration-300"></div>
                </Link>
              ) : (
                <button
                  key={item.name}
                  onClick={() => scrollToSection(item.id)}
                  className="relative text-sm font-medium text-muted-foreground hover:text-foreground transition-all duration-300 group"
                >
                  <span className="relative z-10">{item.name}</span>
                  <div className="absolute inset-0 bg-primary/10 rounded-lg scale-0 group-hover:scale-100 transition-transform duration-300 -z-0"></div>
                  <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary group-hover:w-full transition-all duration-300"></div>
                </button>
              )
            ))}
          </div>


          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="sm"
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 pb-4 border-t border-border pt-4 animate-in slide-in-from-top-2 duration-300">
            <div className="flex flex-col gap-4">
              {navItems.map((item) => (
                item.path ? (
                  <Link
                    key={item.name}
                    to={item.path}
                    className="text-left text-sm font-medium text-muted-foreground hover:text-foreground transition-colors duration-200 py-2 px-4 hover:bg-primary/10 rounded-lg flex items-center gap-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {item.name === 'Documentation' && <BookOpen className="h-4 w-4" />}
                    {item.name}
                  </Link>
                ) : (
                  <button
                    key={item.name}
                    onClick={() => scrollToSection(item.id)}
                    className="text-left text-sm font-medium text-muted-foreground hover:text-foreground transition-colors duration-200 py-2 px-4 hover:bg-primary/10 rounded-lg"
                  >
                    {item.name}
                  </button>
                )
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
