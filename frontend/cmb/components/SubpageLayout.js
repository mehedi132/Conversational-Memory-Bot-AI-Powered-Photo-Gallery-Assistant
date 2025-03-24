import Navbar from "../components/Navbar";
import Footer from "../components/Footer";const SubpageLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-blue-200 flex flex-col">
      <Navbar />
      <main className="flex-1 pt-16">{children}</main>
    
    </div>
  );
};

export default SubpageLayout;