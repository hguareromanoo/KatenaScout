/**
 * Search utility functions
 */

/**
 * Filter items based on a search term
 * 
 * @param {Array} items - Array of items to filter
 * @param {string} searchTerm - Term to search for
 * @param {Array} fields - Fields to search in (default: ['name'])
 * @returns {Array} - Filtered items
 */
export const filterItems = (items, searchTerm, fields = ['name']) => {
  if (!items || !Array.isArray(items) || !searchTerm) return items;
  
  const term = searchTerm.toLowerCase().trim();
  if (!term) return items;
  
  return items.filter(item => {
    return fields.some(field => {
      const value = item[field];
      if (!value) return false;
      
      if (typeof value === 'string') {
        return value.toLowerCase().includes(term);
      }
      
      if (Array.isArray(value)) {
        return value.some(v => 
          typeof v === 'string' && v.toLowerCase().includes(term)
        );
      }
      
      return false;
    });
  });
};

/**
 * Sort items by a specific field
 * 
 * @param {Array} items - Array of items to sort
 * @param {string} field - Field to sort by
 * @param {boolean} ascending - Sort direction (default: true)
 * @returns {Array} - Sorted items
 */
export const sortItems = (items, field, ascending = true) => {
  if (!items || !Array.isArray(items) || !field) return items;
  
  return [...items].sort((a, b) => {
    let aValue = a[field];
    let bValue = b[field];
    
    // Handle undefined or null values
    if (aValue === undefined || aValue === null) return ascending ? -1 : 1;
    if (bValue === undefined || bValue === null) return ascending ? 1 : -1;
    
    // Handle numbers
    if (typeof aValue === 'number' && typeof bValue === 'number') {
      return ascending ? aValue - bValue : bValue - aValue;
    }
    
    // Convert to strings for comparison
    aValue = String(aValue).toLowerCase();
    bValue = String(bValue).toLowerCase();
    
    return ascending 
      ? aValue.localeCompare(bValue) 
      : bValue.localeCompare(aValue);
  });
};

/**
 * Group items by a specific field
 * 
 * @param {Array} items - Array of items to group
 * @param {string} field - Field to group by
 * @returns {Object} - Grouped items
 */
export const groupItems = (items, field) => {
  if (!items || !Array.isArray(items) || !field) return {};
  
  return items.reduce((groups, item) => {
    const key = item[field];
    if (!key) return groups;
    
    // Convert arrays to strings for grouping
    const groupKey = Array.isArray(key) ? key.join(', ') : String(key);
    
    if (!groups[groupKey]) {
      groups[groupKey] = [];
    }
    
    groups[groupKey].push(item);
    return groups;
  }, {});
};

/**
 * Extract unique values for a field from an array of items
 * 
 * @param {Array} items - Array of items
 * @param {string} field - Field to extract values from
 * @returns {Array} - Array of unique values
 */
export const extractUniqueValues = (items, field) => {
  if (!items || !Array.isArray(items) || !field) return [];
  
  const values = new Set();
  
  items.forEach(item => {
    const value = item[field];
    
    if (value === undefined || value === null) return;
    
    if (Array.isArray(value)) {
      value.forEach(v => {
        if (v !== undefined && v !== null) {
          values.add(v);
        }
      });
    } else {
      values.add(value);
    }
  });
  
  return [...values];
};