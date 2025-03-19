/**
 * Date utility functions
 */

/**
 * Format a date to a readable string
 * 
 * @param {string|Date} date - Date to format
 * @param {string} locale - Locale to use for formatting
 * @returns {string} - Formatted date string
 */
export const formatDate = (date, locale = 'en-US') => {
  try {
    if (!date) return '';
    
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    
    // Check if date is valid
    if (isNaN(dateObj.getTime())) return '';
    
    return dateObj.toLocaleDateString(locale, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch (error) {
    console.error('Error formatting date:', error);
    return '';
  }
};

/**
 * Calculate age from birth date
 * 
 * @param {string|Date} birthDate - Birth date
 * @returns {number|null} - Age in years or null if invalid
 */
export const calculateAge = (birthDate) => {
  try {
    if (!birthDate) return null;
    
    const birthDateObj = typeof birthDate === 'string' ? new Date(birthDate) : birthDate;
    
    // Check if date is valid
    if (isNaN(birthDateObj.getTime())) return null;
    
    const today = new Date();
    let age = today.getFullYear() - birthDateObj.getFullYear();
    const monthDiff = today.getMonth() - birthDateObj.getMonth();
    
    // Adjust age if birthday hasn't occurred yet this year
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDateObj.getDate())) {
      age--;
    }
    
    return age;
  } catch (error) {
    console.error('Error calculating age:', error);
    return null;
  }
};

/**
 * Format a date range to a readable string
 * 
 * @param {string|Date} startDate - Start date
 * @param {string|Date} endDate - End date
 * @param {string} locale - Locale to use for formatting
 * @returns {string} - Formatted date range string
 */
export const formatDateRange = (startDate, endDate, locale = 'en-US') => {
  try {
    if (!startDate || !endDate) return '';
    
    const start = formatDate(startDate, locale);
    const end = formatDate(endDate, locale);
    
    return `${start} - ${end}`;
  } catch (error) {
    console.error('Error formatting date range:', error);
    return '';
  }
};