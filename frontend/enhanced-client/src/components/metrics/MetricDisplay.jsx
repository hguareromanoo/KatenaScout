import React from 'react';
import { useTranslation } from 'react-i18next';
import { 
  formatMetricName, 
  getMetricCategory, 
  getMetricIcon, 
  isPercentageMetric 
} from '../../utils/formatters';

/**
 * Formata o valor da métrica baseado em seu tipo
 */
const formatMetricValue = (key, value) => {
  if (value === undefined || value === null) return '-';
  
  if (isPercentageMetric(key)) {
    return `${value.toFixed(1)}%`;
  }
  
  if (typeof value === 'number') {
    // Valores inteiros não precisam de casas decimais
    return Number.isInteger(value) ? value.toString() : value.toFixed(2);
  }
  
  return value.toString();
};

/**
 * Componente para exibir estatísticas do jogador com ícone e tradução
 */
const MetricDisplay = ({ 
  metricKey, 
  value, 
  showIcon = true, 
  showCategory = false,
  showUnit = true
}) => {
  const { t } = useTranslation();
  const category = getMetricCategory(metricKey);
  const iconName = getMetricIcon(metricKey);
  const formattedName = formatMetricName(metricKey, t, { showUnit });
  const formattedValue = formatMetricValue(metricKey, value);
  
  return (
    <div className={`metric-display metric-${category}`}>
      {showIcon && (
        <div className="metric-icon-container">
          <span className={`icon icon-${iconName}`}></span>
        </div>
      )}
      
      <div className="metric-content">
        <div className="metric-name">{formattedName}</div>
        <div className="metric-value">{formattedValue}</div>
        
        {showCategory && (
          <div className="metric-category-label">
            {t(`metrics.categories.${category}`)}
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricDisplay;