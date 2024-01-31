import React, {
  useState,
  useEffect,
  useCallback
} from 'react';
import {
  Box,
  Container,
} from '@mui/material';
import { makeStyles } from '@mui/styles';
import axios from '../../../utils/axios';
import Page from '../../../components/Page';
import useIsMountedRef from '../../../hooks/useIsMountedRef';
import Header from './Header';
import Results from './Results';

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingTop: theme.spacing(3),
    paddingBottom: theme.spacing(3)
  }
}));

function CustomerListView() {
  const classes = useStyles();
  const isMountedRef = useIsMountedRef();
  const [customers, setCustomers] = useState(null);

  const getCustomers = useCallback(() => {
    axios
      .get('/api/management/customers')
      .then((response) => {
        if (isMountedRef.current) {
          setCustomers(response.data.customers);
        }
      });
  }, [isMountedRef]);

  useEffect(() => {
    getCustomers();
  }, [getCustomers]);

  if (!customers) {
    return null;
  }

  return (
    <Page
      className={classes.root}
      title="Customer List"
    >
      <Container maxWidth={false}>
        <Header />
        {customers && (
          <Box mt={3}>
            <Results customers={customers} />
          </Box>
        )}
      </Container>
    </Page>
  );
}

export default CustomerListView;
