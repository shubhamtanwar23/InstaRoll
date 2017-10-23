import React from 'react';
import { Image } from 'react-native';
import Card from './card';
import CardSection from './card-section';
import Button from './button';
import Input from './input';

export default class SelectForm extends React.Component {
	render() {
		return(
			<Card>
				<CardSection>
					<Input 
						label='Name'
						value={this.props.text}
						onChangeText={this.props.onChangeText}
					/>
				</CardSection>
				<CardSection>
					<Image 
						source={this.props.imageSource}
						style={{height: 300, width: null, flex: 1}}
					/>
				</CardSection>
				<CardSection>
					<Button onPress={this.props.onPress}>
						Select Photo
					</Button>
				</CardSection>
			</Card>
		);
	}
}