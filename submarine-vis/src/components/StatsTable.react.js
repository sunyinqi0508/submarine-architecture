import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';

const styles = () => ({
  root: {
    width: '20%',
    marginLeft: '20%',
    marginTop: '10%',
    overflowX: 'auto',
    height: '50%',
  },
  table: {
    minWidth: 300,
  },
  colorBox: {
    width: '20px',
    height: '20px',
  },
});


const formatRow = (key, title, value) => (
    <TableRow key={key}>
        <TableCell component="th" scope="row">
        <Typography variant="body2">
            {title}
        </Typography>
        </TableCell>
        <TableCell>{value}</TableCell>
    </TableRow>
); 

function StatsTable(props) {
  const { classes } = props;

  const getColorBox = (region) => (<div className={classes.colorBox} style={{backgroundColor: region === 'red' ? '#ef0e0e' : '#efdc0e'}} />);

  return (
    <Paper className={classes.root}>
      <Table className={classes.table}>
        <TableBody>
            {formatRow(1, 'Red Region', `${props.redRegion} - ${props.redRegion + 5}`)}
            {formatRow(2, 'Submarine Position', props.position)}
            {formatRow(3, 'Submarine Region', getColorBox(props.submarineRegion))}
            {formatRow(4, 'Trench Manager Alert', getColorBox(props.trenchAlert))}
            {formatRow(5, 'Safety Condition Achieved?', props.isSafetyConditionAchieved ? 'yes' : 'no')}
            {formatRow(6, 'Current Set of Probes', props.probes.toString())}
        </TableBody>
      </Table>
    </Paper>
  );
}

StatsTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(StatsTable);