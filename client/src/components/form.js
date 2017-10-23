import React from 'react';
import { Image, View } from 'react-native';
import Card from './card';
import CardSection from './card-section';
import Button from './button';
import Input from './input';
import SelectForm from './select-form';
import UploadForm from './upload-form';

export default class Form extends React.Component {
	constructor(props) {
		super(props);
		this.state = {text: '', imageSource: require('../../res/img/flower.jpg'), imageHasSelected: false};
		this.onPressSelectHandler = this.onPressSelectHandler.bind(this);
		this.onPressUploadHandler = this.onPressUploadHandler.bind(this);

	}

	onPressUploadHandler() {
		console.log('Uploading the photo');
	}

	onPressSelectHandler() {
		this.setState({imageHasSelected: true});
	}

	render() {
		return(
			<View>
				{this.state.imageHasSelected ?
				    <UploadForm 
						value= {this.state.text}
						onChangeText= {text => this.setState({text})}
						imageSource= {this.state.imageSource} 
						onPress= {this.onPressUploadHandler}
					/> : 
					<SelectForm onPress={this.onPressSelectHandler} />
				}
			</View>
		);
	}
}
