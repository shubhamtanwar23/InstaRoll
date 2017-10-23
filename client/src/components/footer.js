import React from 'react';
import { Text, View } from 'react-native';


export default class Footer extends React.Component {
	 

	render() {
		return (
			<View style={styles.viewStyle}>
				<Text style={styles.textStyle}> Made by Shubham Tanwar with love ❤️</Text>
			</View>
		);
	}
}

const styles = {
	textStyle: {
		fontSize: 16,
		fontFamily: 'serif',
		fontStyle: 'italic',
		color: 'cornflowerblue'
	},
	viewStyle: {
		justifyContent: 'center',
		alignItems: 'center',
		backgroundColor: '#F8F8F8',
		height: 60,
	}
};
