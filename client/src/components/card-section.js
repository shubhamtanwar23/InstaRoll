import React from 'react';
import { View } from 'react-native';

// Create a component

export default class CardSection extends React.Component {
  
  render() {
    return (
      <View style={styles.containerStyle}>
        {this.props.children}
      </View>
    );
  }
};

const styles = {
  containerStyle: {
    borderBottomWidth: 1,
    padding: 5,
    justifyContent: 'flex-start',
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderColor: '#ddd',
    position: 'relative'
  }
};
