import React, {
  useState,
  useCallback,
  useEffect
} from 'react';
import {
  Box,
  Container,
  makeStyles
} from '@mui/material';
import axios from '../../../utils/axios';
import Page from '../../../components/Page';
import useIsMountedRef from '../../../hooks/useIsMountedRef';
import CustomerEditForm from './CustomerEditForm';
import Header from './Header';

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingTop: theme.spacing(3),
    paddingBottom: theme.spacing(3)
  }
}));

function CustomerEditView() {
  const classes = useStyles();
  const isMountedRef = useIsMountedRef();
  const [customer, setCustomer] = useState();

  const getCustomer = useCallback(() => {
    axios
      .get('/api/management/customers/1')
      .then((response) => {
        if (isMountedRef.current) {
          setCustomer(response.data.customer);
        }
      });
  }, [isMountedRef]);

  useEffect(() => {
    getCustomer();
  }, [getCustomer]);

  if (!customer) {
    return null;
  }

  return (
    <Page
      className={classes.root}
      title="Customer Edit"
    >
      <Container maxWidth="lg">
        <Header />
        <Box mt={3}>
          <CustomerEditForm customer={customer} />
        </Box>
      </Container>
    </Page>
  );
}

export default CustomerEditView;
