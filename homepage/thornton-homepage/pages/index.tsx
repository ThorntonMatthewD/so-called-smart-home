import type { NextPage } from 'next';
import Head from 'next/head';
import styles from '../styles/Home.module.css';

import services from '../data/services';
import GridItem from '../components/grid-item';
import { Service } from '../interfaces/home.interfaces';

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>The Thornton Digital Homestead</title>
        <meta name="description" content="The portal to the Thornton Family's Intranet" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to The Thornton Digital Homestead
        </h1>

        <div className={styles.grid}>
          {services.map((service: Service) => {
            console.log(service)
            return <GridItem key={service.url} service={service} />
          })
        } 
        </div>
      </main>
    </div>
  )
}

export default Home;
