import React, { FunctionComponent, Suspense } from 'react'
import Image from 'next/image'

import styles from '../styles/Home.module.css'
import { Service } from '../interfaces/home.interfaces';


type Props = {
  service: Service
}

const GridItem: FunctionComponent<Props> = ({ service }) => {

  return ( 
    <a href={service.url} className={styles.card}>
      <h2>{service.name} &rarr;</h2>
      {service.img_src && (
        <Image src={service.img_src} alt={service.name} width={100} height={100}/>
      )}
      <p>{service.description}</p>
    </a>
  )
}

export default GridItem;