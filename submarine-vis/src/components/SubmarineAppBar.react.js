import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

const styles = {
    root: {
      flexGrow: 1,
    },
    grow: {
      flexGrow: 1,
    },
  };

  
function SubmarineAppBar(props) {
    const { classes } = props;
    return (
      <div className={classes.root}>
        <AppBar position="static" style={{backgroundColor: '#d80d0d'}}>
          <Toolbar>
            <Typography variant="title" color="inherit" className={classes.grow}>
                Submarine Alert
            </Typography>
          </Toolbar>
        </AppBar>
      </div>
    );
  }

  SubmarineAppBar.propTypes = {
    classes: PropTypes.object.isRequired,
  };
  
  export default withStyles(styles)(SubmarineAppBar);
