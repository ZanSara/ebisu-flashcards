import "../global.css";
import { AppProps } from "next/app";

const EbisuWeb = ({ Component, pageProps }: AppProps) => {
  // We decorate the page with an outer div,
  // which gives some padding to the content (except mobile)
  return (
    <div id="paddingBox" className="flex-grow flex flex-col md:p-10">
      <Component {...pageProps} />
    </div>
  );
};

export default EbisuWeb;
