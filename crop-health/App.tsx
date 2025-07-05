import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import ImagePickerScreen from './src/presentation/pages/ImagePickerScreen';
import DiagnosisResultScreen from './src/presentation/pages/DiagnosisResultScreen';
import { RootStackParamList } from './src/navigation/RootNavigator';

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen
          name="Home"
          component={ImagePickerScreen}
          options={{ title: 'Plant Disease Detector' }}
        />
        <Stack.Screen
          name="Result"
          component={DiagnosisResultScreen}
          options={{ title: 'Result' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
