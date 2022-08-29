import React, { FunctionComponent } from 'react'
import styles from '../styles/Home.module.css'
import { Service } from '../interfaces/home.interfaces';

type Props = {
  service: Service
}

const GridItem: FunctionComponent<Props> = ({ service }) => {

  return ( 
    <a href={service.url} className={styles.card}>
      <h2>{service.name} &rarr;</h2>
      <p>{service.description}</p>
    </a>
  )
}

export default GridItem;