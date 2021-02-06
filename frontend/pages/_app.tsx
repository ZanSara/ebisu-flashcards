import 'tailwindcss/tailwind.css'
import {AppProps} from "next/app";

const EbisuWeb = ({ Component, pageProps }: AppProps) => {
    return <Component {...pageProps} />
}

export default EbisuWeb;