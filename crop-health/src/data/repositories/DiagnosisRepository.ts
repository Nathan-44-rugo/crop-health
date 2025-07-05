import { DiagnosisRepository } from '../../domain/repositories/DiagnosisRepository';
import { DiagnosisResult } from '../../domain/entities/DiagnosisResult';
import axios from 'axios';

export class DiagnosisRepositoryImpl implements DiagnosisRepository {
    private api = process.env.BACKEND_URL;

    async diagnose(imageUri: string): Promise<DiagnosisResult> {
        const formData = new FormData();
        const fileName = imageUri.split('/').pop() || 'leaf.jpg';
        const fileType = fileName.split('.').pop();

        formData.append('image', {
        uri: imageUri,
        type: `image/${fileType}`,
        name: fileName,
        } as any);

        const response = await axios.post(`${this.api}/diagnose`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        });

        return {
        diseaseName: response.data.diseaseName,
        treatmentAdvice: response.data.treatmentAdvice,
        };
    }
}
