import React from 'react';
import {
  SafeAreaView, ScrollView, View, Text, StyleSheet, Button, Platform,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../navigation/RootNavigator';
import { stripMarkdown } from '../../utils/text';

type Props = NativeStackScreenProps<RootStackParamList, 'Result'>;

const DiagnosisResultScreen: React.FC<Props> = ({ route, navigation }) => {
  const { diseaseName, confidence, treatmentAdvice, logId } = route.params;
  const formattedConfidence = (confidence * 100).toFixed(1);
  const plainAdvice = stripMarkdown(treatmentAdvice);

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.title}>Diagnosis Result</Text>
        {/* Disease */}
        <View style={styles.card}>
          <Text style={styles.label}>🦠 Disease Detected</Text>
          <Text style={styles.value}>{diseaseName.replace(/___/g, ' ')}</Text>
        </View>
        {/* Confidence */}
        <View style={styles.card}>
          <Text style={styles.label}>✅ Confidence</Text>
          <Text style={styles.value}>{formattedConfidence}%</Text>
        </View>
        {/* Treatment Advice */}
        <View style={styles.card}>
          <Text style={styles.label}>💡 Treatment Advice</Text>
          <Text style={styles.value}>{plainAdvice}</Text>
        </View>
        {/* Log ID */}
        <View style={styles.card}>
          <Text style={styles.label}>📝 Log Reference</Text>
          <Text style={[styles.value, styles.logId]} selectable>
            {logId}
          </Text>
        </View>
        {/* Back Button */}
        <View style={styles.buttonWrap}>
          <Button
            title="🔙 Back to Scan"
            onPress={() => navigation.popToTop()}
            color={Platform.OS === 'ios' ? undefined : '#FF3B30'}
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

// styles unchanged from previous version

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#EFF1F3',
  },
  container: {
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: Platform.OS === 'ios' ? '600' : 'bold',
    marginBottom: 20,
    color: '#1A1A1A',
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
        shadowOpacity: 0.06,
        shadowRadius: 8,
        shadowOffset: { width: 0, height: 4 },
      },
      android: {
        elevation: 2,
      },
    }),
  },
  label: {
    fontSize: 18,
    fontWeight: '500',
    color: '#444444',
  },
  value: {
    fontSize: 16,
    marginTop: 6,
    color: '#2C2C2C',
  },
  advice: {
    fontStyle: 'italic',
    lineHeight: 22,
  },
  logId: {
    fontSize: 14,
    color: '#555555',
  },
  buttonWrap: {
    marginTop: 30,
    width: '100%',
  },
});

export default DiagnosisResultScreen;
