import React from 'react';
import {
    SafeAreaView,
    View,
    Text,
    StyleSheet,
    Button,
    ScrollView,
    Platform,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../navigation/RootNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'Result'>;

const DiagnosisResultScreen: React.FC<Props> = ({ route, navigation }) => {
    const { diseaseName, treatmentAdvice } = route.params;

    return (
        <SafeAreaView style={styles.safeArea}>
        <ScrollView contentContainerStyle={styles.container}>
            <Text style={styles.title}>Diagnosis Result</Text>
            <View style={styles.card}>
            <Text style={styles.label}>Disease:</Text>
            <Text style={styles.value}>{diseaseName}</Text>
            </View>
            <View style={styles.card}>
            <Text style={styles.label}>Treatment Advice:</Text>
            <Text style={styles.value}>{treatmentAdvice}</Text>
            </View>
            <View style={styles.buttonWrap}>
            <Button
                title="🔙 Back"
                onPress={() => navigation.popToTop()}
                color={Platform.OS === 'ios' ? undefined : '#FF3B30'}
            />
            </View>
        </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    safeArea: {
        flex: 1,
        backgroundColor: '#FFFFFF',
    },
    container: {
        padding: 16,
        alignItems: 'center',
    },
    title: {
        fontSize: 26,
        fontWeight: Platform.OS === 'ios' ? '600' : 'bold',
        marginBottom: 20,
        color: '#1C1C1E',
    },
    card: {
        width: '100%',
        padding: 16,
        marginVertical: 8,
        backgroundColor: '#F9F9F9',
        borderRadius: 10,
        ...Platform.select({
        ios: {
            shadowColor: '#000',
            shadowOpacity: 0.08,
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
        color: '#333333',
    },
    value: {
        fontSize: 16,
        marginTop: 6,
        color: '#1C1C1E',
    },
    buttonWrap: {
        marginTop: 30,
        width: '100%',
    },
});

export default DiagnosisResultScreen;
