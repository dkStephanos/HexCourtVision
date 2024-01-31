import React, { useState, useRef } from 'react';
import { useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import {
  Box,
  Card,
  CardContent,
  Divider,
  IconButton,
  Input,
  Paper,
  Tooltip,
} from '@mui/material';
import { makeStyles } from '@mui/styles';
import SendIcon from '@mui/icons-material/Send';
import AddPhotoIcon from '@mui/icons-material/AddPhotoAlternate';
import AttachFileIcon from '@mui/icons-material/AttachFile';

const useStyles = makeStyles(() => ({
  root: {},
  divider: {
    width: 1,
    height: 24
  },
  fileInput: {
    display: 'none'
  }
}));

function PostAdd({ className, ...rest }) {
  const classes = useStyles();
  const fileInputRef = useRef(null);
  const [value, setValue] = useState('');
  const account = useSelector((state) => state.account);

  const handleChange = (event) => {
    event.persist();
    setValue(event.target.value);
  };

  const handleAttach = () => {
    fileInputRef.current.click();
  };

  return (
    <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
      <CardContent>
        <Box
          display="flex"
          alignItems="center"
        >
          <Paper
            component={Box}
            flexGrow={1}
            py={0.5}
            px={2}
            variant="outlined"
          >
            <Input
              disableUnderline
              fullWidth
              onChange={handleChange}
              placeholder={`What's on your mind, ${account.user.firstName}`}
            />
          </Paper>
          <Tooltip title="Send">
            <IconButton color={value.length > 0 ? 'primary' : 'default'}>
              <SendIcon />
            </IconButton>
          </Tooltip>
          <Divider className={classes.divider} />
          <Tooltip title="Attach image">
            <IconButton
              edge="end"
              onClick={handleAttach}
            >
              <AddPhotoIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Attach file">
            <IconButton
              edge="end"
              onClick={handleAttach}
            >
              <AttachFileIcon />
            </IconButton>
          </Tooltip>
          <input
            className={classes.fileInput}
            ref={fileInputRef}
            type="file"
          />
        </Box>
      </CardContent>
    </Card>
  );
}

PostAdd.propTypes = {
  className: PropTypes.string
};

export default PostAdd;
