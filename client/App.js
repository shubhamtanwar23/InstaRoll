/**
 * App.js
 */

import React from 'react';
import { AppRegistry, View, Text, ScrollView } from 'react-native';
import Header from './src/components/header';
import Form from './src/components/form';
import Footer from './src/components/footer';


// Create React Component called App
export default class App extends React.Component {
  render() {
    return (
        <View style={{flex: 1}}>
          <Header text="Insta Roll"/>
          <ScrollView>
          	<Form />
          </ScrollView>
          <Footer />
        </View>
      ); 
  }
}

// Render it to the device
AppRegistry.registerComponent('instaroll', () => <App />);