/**
 * header.js
 * Implementation of Header component
 */

import React from 'react';
import { Text, View } from 'react-native';


export default class Header extends React.Component {
	constructor(props) {
		super(props);
		const { textStyle, viewStyle } = styles;

	}

	render() {
		return (
			<View style={styles.viewStyle}>
				<Text style={styles.textStyle}>  {this.props.text} </Text>
			</View>
		);
	}
}

const styles = {
	textStyle: {
		fontSize: 24,
		fontFamily: 'serif',
	},
	viewStyle: {
		justifyContent: 'center',
		alignItems: 'center',
		backgroundColor: '#f4f4f4',
		paddingTop: 20,
		height: 80,
		shadowColor: '#ddd',
		shadowOffset: {width: 0, height: 4},
		shadowOpacity: 0.9,
		elevation: 2,
		position: 'relative'
	}
};
