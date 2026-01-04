import React from 'react';
import { ModelInfo } from '../types';

interface ModelSelectorProps {
    models: ModelInfo[];
    selectedProvider: string;
    selectedModel: string;
    onChange: (provider: string, model: string) => void;
    disabled?: boolean;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
    models,
    selectedProvider,
    selectedModel,
    onChange,
    disabled
}) => {
    // Format value as "provider/model" for the select element
    const selectedValue = `${selectedProvider}/${selectedModel}`;

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const [provider, model] = e.target.value.split('/');
        onChange(provider, model);
    };

    return (
        <div className="model-selector">
            <label htmlFor="model-select">AI Model:</label>
            <select
                id="model-select"
                value={selectedValue}
                onChange={handleChange}
                disabled={disabled}
            >
                {models.map((m) => (
                    <option key={`${m.provider}/${m.model}`} value={`${m.provider}/${m.model}`}>
                        {m.display_name}
                    </option>
                ))}
            </select>
        </div>
    );
};
