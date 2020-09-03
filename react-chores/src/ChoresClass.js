import ChoresItem from './components/ChoresItem';
import App from "./App";
import React, {Component} from 'react';

class ChoresClass extends React.Component {

    constructor(props) {
        super(props);
    }

    add_chore_handle() {}
    delete_chore_handle() {}


    render() {
        return(
            <div>
            <h1>Luther Chores Manager</h1>
            <h2>Sunday</h2>
                <ChoresItem name='After Dinner Clean'/>
                <ChoresItem name='Cheffin'/>
                <ChoresItem name='1510 Bathroom Clean'/>
            <h2>Monday</h2>
            <h2>Tuesday</h2>
            <h2>Wednesday</h2>
            <h2>Thursday</h2>
            <h2>Friday</h2>
            <h2>Saturday</h2>
            </div>
        );
    }
}

export default ChoresClass;