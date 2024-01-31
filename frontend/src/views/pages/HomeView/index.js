import React from 'react';
import { makeStyles } from '@mui/styles';
import Page from '../../../components/Page';
import Hero from './Hero';
import Features from './Features';
import Testimonials from './Testimonials';
import CTA from './CTA';
import FAQS from './FAQS';

const useStyles = makeStyles(() => ({
  root: {}
}));

function HomeView() {
  const classes = useStyles();

  return (
    <Page
      className={classes.root}
      title="Home"
    >
      <Hero />
      <Features />
      <Testimonials />
      <CTA />
      <FAQS />
    </Page>
  );
}

export default HomeView;
