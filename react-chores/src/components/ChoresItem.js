import React, {Component} from 'react';

class ChoresItem extends React.Component {

    constructor(props) {
        super(props);
        this.state = {chore_name: props.name, person_name: ''};
    }

    upload_img_handle() {}
    person_name_update_handle() {}
    submit_handle() {}


    render() {
        return(
            <div>
                <div className='child inline-block-child'>
                    <h3>{this.state.chore_name}</h3>
                </div>
                <div className='child inline-block-child'>
                    <input type='text' id='lutherite'/>
                </div>
                <div className='child inline-block-child'>
                    <button onClick={this.upload_img_handle.bind(this)}>Upload Image</button>
                </div>
                <div className='child inline-block-child'>
                    <button onClick={this.submit_handle.bind(this)}>Submit</button>
                </div>
            </div>
        );
    }
}

export default ChoresItem;