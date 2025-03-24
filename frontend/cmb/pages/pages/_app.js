import '@/styles/globals.css'



function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}

export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />
}

