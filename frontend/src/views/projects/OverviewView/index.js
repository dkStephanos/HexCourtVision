import React from 'react';
import {
  Box,
  Container,
} from '@mui/material';
import { makeStyles } from '@mui/styles';
import Page from '../../../components/Page';
import Header from './Header';
import Statistics from './Statistics';
import Notifications from './Notifications';
import Projects from './Projects';
import Todos from './Todos';

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    paddingTop: theme.spacing(3),
    paddingBottom: theme.spacing(3)
  }
}));

function OverviewView() {
  const classes = useStyles();

  return (
    <Page
      className={classes.root}
      title="Overview"
    >
      <Container maxWidth="lg">
        <Header />
        <Box mt={3}>
          <Statistics />
        </Box>
        <Box mt={6}>
          <Notifications />
        </Box>
        <Box mt={6}>
          <Projects />
        </Box>
        <Box mt={6}>
          <Todos />
        </Box>
      </Container>
    </Page>
  );
}

export default OverviewView;
