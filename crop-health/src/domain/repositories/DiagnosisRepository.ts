import { DiagnosisResult } from '../entities/DiagnosisResult';

export interface DiagnosisRepository {
    diagnose(imageUri: string): Promise<DiagnosisResult>;
}
