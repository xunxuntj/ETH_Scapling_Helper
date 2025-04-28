import Head from 'next/head';

export default function Home() {
  return (
    <div>
      <Head>
        <title>ETH Scalping Assistant</title>
        <meta name="description" content="ETH Scalping Assistant Dashboard" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="flex min-h-screen flex-col items-center justify-center py-2">
        <h1 className="text-4xl font-bold">
          Welcome to ETH Scalping Assistant
        </h1>
      </main>
    </div>
  );
}
