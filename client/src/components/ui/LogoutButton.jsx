import { LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "@/core/store/AuthContext";
import Button3D from "@/components/ui/Button3D"; // use 3D button

const LogoutButton = () => {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <Button3D
      onClick={handleLogout}
      variant="warning" // yellow bg
      size="md" // make it spacious
      className="w-full flex items-center justify-center gap-2"
    >
      <LogOut size={18} />
      Logout
    </Button3D>
  );
};

export default LogoutButton;
