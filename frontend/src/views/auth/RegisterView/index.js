import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { Box, Button, Card, CardContent, Container, Divider, Link, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import Page from '../../../components/Page';
import Logo from '../../../components/Logo';
import RegisterForm from './RegisterForm';

const StyledPage = styled(Page)(({ theme }) => ({
  justifyContent: 'center',
  backgroundColor: theme.palette.background.dark,
  display: 'flex',
  height: '100%',
  minHeight: '100%',
  flexDirection: 'column',
  paddingBottom: 80,
  paddingTop: 80
}));

const StyledContainer = styled(Container)({
  // Add any specific styles for the Container here
});

function RegisterView() {
  const navigate = useNavigate();

  const handleSubmitSuccess = () => {
    navigate('/app/login');
  };

  return (
    <StyledPage title="Register">
      <StyledContainer maxWidth="sm">
        <Box
          sx={{
            mb: 5,
            display: 'flex',
            alignItems: 'center'
          }}
        >
          <RouterLink to="/">
            <Logo />
          </RouterLink>
          <Button
            component={RouterLink}
            to="/"
            sx={{ /* Add styles for backButton here if needed */ }}
          >
            Back to home
          </Button>
        </Box>
        <Card>
          <CardContent>
            <Typography
              gutterBottom
              variant="h2"
              color="textPrimary"
            >
              Sign up
            </Typography>
            <Typography variant="subtitle1">
              Sign up on the internal platform
            </Typography>
            <Box mt={3}>
              <RegisterForm onSubmitSuccess={handleSubmitSuccess} />
            </Box>
            <Box my={2}>
              <Divider />
            </Box>
            <Link
              component={RouterLink}
              to="/login"
              variant="body2"
              color="textSecondary"
            >
              Have an account?
            </Link>
          </CardContent>
        </Card>
      </StyledContainer>
    </StyledPage>
  );
}

export default RegisterView;
