import React, { useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import MetricDisplay from './MetricDisplay';
import { getMetricCategory } from '../../utils/formatters';

/**
 * Exibe uma grade de métricas organizadas por categorias
 */
const MetricsGrid = ({ 
  metrics = {}, 
  showIcons = true,
  showCategories = true,
  columns = 1,
  filter = null
}) => {
  const { t } = useTranslation();
  
  const categorizedMetrics = useMemo(() => {
    const result = {};
    
    // Filtrar métricas se necessário
    const filteredMetrics = filter 
      ? Object.entries(metrics).filter(([key]) => filter(key))
      : Object.entries(metrics);
      
    // Agrupar por categoria
    filteredMetrics.forEach(([key, value]) => {
      const category = getMetricCategory(key);
      
      if (!result[category]) {
        result[category] = [];
      }
      
      result[category].push({ key, value });
    });
    
    return result;
  }, [metrics, filter]);
  
  return (
    <div className="metrics-grid">
      {Object.entries(categorizedMetrics).map(([category, items]) => (
        <div key={category} className="metrics-category-section">
          {showCategories && (
            <h3 className="metrics-category-title">
              {t(`metrics.categories.${category}`)}
            </h3>
          )}
          
          <div 
            className="metrics-items-grid" 
            style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}
          >
            {items.map(({ key, value }) => (
              <MetricDisplay
                key={key}
                metricKey={key}
                value={value}
                showIcon={showIcons}
                showCategory={false}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default MetricsGrid;