import React from 'react';
import ReactDOM from 'react-dom';
import './assets/css/index.css';
import App from './components/App';
import registerServiceWorker from './assets/registerServiceWorker';

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
