import "../styles/global.css";
import githubLogo from "../assets/github.svg";

const Footer = () => {
  return (
    <footer className="footer">
      <a
        href="https://github.com/evanboyd31/nhl-degrees-of-separation"
        target="_blank"
        rel="noopener noreferrer"
      >
        <img src={githubLogo} alt="Github link" className="github-logo" />
      </a>
    </footer>
  );
};

export default Footer;
