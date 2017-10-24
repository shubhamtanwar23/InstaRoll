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
		this.state = {
			text: '',
			avatarSource: '',
			hasImage: false,
			url: 'https://postman-echo.com/post'
		};
		this.onPressSelectHandler = this.onPressSelectHandler.bind(this);
		this.onPressUploadHandler = this.onPressUploadHandler.bind(this);

	}

	onPressUploadHandler() {
		
		console.log('Uploading the photo');
	}

	onPressSelectHandler() {
		var ImagePicker = require('react-native-image-picker');

		// More info on all the options is below in the README...just some common use cases shown here
		var options = {
		  title: 'Select Avatar',
		  customButtons: [
		    {name: 'fb', title: 'Choose Photo from Facebook'},
		  ],
		  storageOptions: {
		    skipBackup: true,
		    path: 'images'
		  }
		};

		/**
		 * The first arg is the options object for customization (it can also be null or omitted for default options),
		 * The second arg is the callback which sends object: response (more info below in README)
		 */
		ImagePicker.showImagePicker(options, (response) => {
		  console.log('Response = ', response);

		  if (response.didCancel) {
		    console.log('User cancelled image picker');
		  }
		  else if (response.error) {
		    console.log('ImagePicker Error: ', response.error);
		  }
		  else if (response.customButton) {
		    console.log('User tapped custom button: ', response.customButton);
		  }
		  else {
		    let source = { uri: response.uri };

		    // You can also display the image using data:
		    // let source = { uri: 'data:image/jpeg;base64,' + response.data };
		    console.log('Image Source: ' + source);

		    this.setState({
		      avatarSource: source,
		      hasImage: true
		    });
		  }
		});
	}

	render() {
		return(
			<View>
				{this.state.hasImage ?
				    <UploadForm 
						value= {this.state.text}
						onChangeText= {text => this.setState({text})}
						imageSource= {this.state.avatarSource} 
						onPress= {this.onPressUploadHandler}
					/> : 
					<SelectForm onPress={this.onPressSelectHandler} />
				}
			</View>
		);
	}
}
