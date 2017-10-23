import React from 'react';
import {View, Text, TextInput } from 'react-native';

export default class Input extends React.Component {

	render() {
		return(
			<View style={styles.containerStyle}>
				<Text style={styles.labelStyle}>{this.props.label}</Text>
				<TextInput
					value={this.props.value}
					onChangeText={this.props.onChangeText}
					style={styles.inputStyle}
				/>
			</View>
		);
	}
}

const styles = {
	inputStyle: {
		color: '#000',
		paddingRight: 5,
		paddingLeft: 5,
		fontSize: 18,
		lineHeight: 23,
		flex: 2
	},
	labelStyle: {
		fontSize: 18,
		paddingLeft: 5,
		flex: 1
	},
	containerStyle: {
		height: 40,
		flex: 1,
		flexDirection: 'row',
		alignItems: 'center'
	}

};