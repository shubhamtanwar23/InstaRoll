import React from 'react';
import Card from './card';
import CardSection from './card-section';
import Button from './button';

export default class SelectForm extends React.Component {
	render() {
		return(
			<Card>
				<CardSection>
					<Button onPress={this.props.onPress}>
						Select Photo
					</Button>
				</CardSection>
			</Card>
		);
	}
}