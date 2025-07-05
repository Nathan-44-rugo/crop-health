// src/application/usecases/DiagnoseLeafUseCase.ts
import { DiagnosisResult } from '../../domain/entities/DiagnosisResult';
import { DiagnosisRepository } from '../repositories/DiagnosisRepository'

export class DiagnoseLeafUseCase {
    constructor(private diagnosisRepo: DiagnosisRepository) {}

    async execute(imageUri: string): Promise<DiagnosisResult> {
        return this.diagnosisRepo.diagnose(imageUri);
    }
}
