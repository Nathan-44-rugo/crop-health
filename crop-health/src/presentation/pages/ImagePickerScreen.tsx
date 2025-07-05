// src/screens/ImagePickerScreen.tsx

import React, { useState, useCallback, useEffect } from 'react';
import {
  SafeAreaView,
  ScrollView,
  View,
  Button,
  Image,
  StyleSheet,
  Text,
  ActivityIndicator,
  Alert,
  RefreshControl,
  Platform,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { NativeStackScreenProps } from '@react-navigation/native-stack';

import { DiagnoseLeafUseCase } from '../../domain/usecases/DiagnoseLeftUsecase';
import { DiagnosisRepositoryImpl } from '../../data/repositories/DiagnosisRepository';
import { RootStackParamList } from '../../navigation/RootNavigator';

const diagnoseUseCase = new DiagnoseLeafUseCase(new DiagnosisRepositoryImpl());

type Props = NativeStackScreenProps<RootStackParamList, 'Home'>;

const ImagePickerScreen: React.FC<Props> = ({ navigation }) => {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const pickImage = async (fromCamera = false) => {
    let result: ImagePicker.ImagePickerResult;
    if (fromCamera) {
      const { granted } = await ImagePicker.requestCameraPermissionsAsync();
      if (!granted) {
        return Alert.alert('Permission Denied', 'Camera access is required.');
      }
      result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        quality: 1,
      });
    } else {
      result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        quality: 1,
      });
    }
    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
    }
  };

  const diagnose = async () => {
    if (!imageUri) {
      return Alert.alert('No Image', 'Please pick or take a photo first.');
    }
    setLoading(true);
    try {
      const { diseaseName, treatmentAdvice } = await diagnoseUseCase.execute(imageUri);
      navigation.navigate('Result', { diseaseName, treatmentAdvice });
    } catch (err) {
      console.error(err);
      Alert.alert('Error', 'Failed to diagnose image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    setImageUri(null);
    setTimeout(() => setRefreshing(false), 500);
  }, []);

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        contentContainerStyle={styles.container}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        <Text style={styles.title}>Plant Disease Detector</Text>

        <View style={styles.card}>
          <Button
            title="📷 Take Photo"
            onPress={() => pickImage(true)}
            color={Platform.OS === 'ios' ? undefined : '#007AFF'}
          />
          <View style={styles.spacer} />
          <Button
            title="🖼️ Choose from Gallery"
            onPress={() => pickImage(false)}
            color={Platform.OS === 'ios' ? undefined : '#007AFF'}
          />
        </View>

        {imageUri && (
          <View style={styles.previewCard}>
            <Image source={{ uri: imageUri }} style={styles.image} />
          </View>
        )}

        {imageUri && !loading && (
          <View style={styles.card}>
            <Button
              title="🩺 Diagnose"
              onPress={diagnose}
              color={Platform.OS === 'ios' ? undefined : '#34C759'}
            />
          </View>
        )}

        {loading && <ActivityIndicator size="large" style={styles.loader} />}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#F2F2F7',
  },
  container: {
    padding: 16,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: Platform.OS === 'ios' ? '600' : 'bold',
    marginBottom: 20,
    color: '#1C1C1E',
  },
  card: {
    width: '100%',
    padding: 16,
    marginVertical: 8,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOpacity: 0.1,
        shadowRadius: 10,
        shadowOffset: { width: 0, height: 5 },
      },
      android: {
        elevation: 3,
      },
    }),
  },
  previewCard: {
    width: 300,
    height: 300,
    marginVertical: 16,
    borderRadius: 12,
    overflow: 'hidden',
    backgroundColor: '#FFFFFF',
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOpacity: 0.1,
        shadowRadius: 10,
        shadowOffset: { width: 0, height: 5 },
      },
      android: {
        elevation: 3,
      },
    }),
  },
  image: {
    width: '100%',
    height: '100%',
  },
  spacer: { height: 10 },
  loader: { marginTop: 20 },
});

export default ImagePickerScreen;
