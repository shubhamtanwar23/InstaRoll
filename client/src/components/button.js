import React from 'react';
import { TouchableOpacity, Text } from 'react-native';

// Create a component

export default class Button extends React.Component {
  constructor(props) {
    super(props);
  }
  
  render() {
    return (
    <TouchableOpacity 
      onPress={this.props.onPress} 
      style={styles.buttonStyle}
    >
      <Text style={styles.textStyle}>
        {this.props.children}
      </Text>
    </TouchableOpacity>
  );
  }
};

const styles = {
  textStyle:{
    alignSelf: 'center',
    color: '#007aff',
    fontSize: 16,
    fontWeight: '600',
    paddingTop: 10,
    paddingBottom: 10
  },
  buttonStyle:{
    flex: 1,
    alignSelf: 'stretch',
    backgroundColor: '#fff',
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#007aff',
    marginLeft: 5,
    marginRight: 5
  }
};
