import { useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';

export const useRealtime = (tableName) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    // 1. Initial Fetch
    const fetchData = async () => {
      const { data: initialData } = await supabase.from(tableName).select('*');
      setData(initialData);
    };
    fetchData();

    // 2. Subscribe to Changes
    const channel = supabase
      .channel('schema-db-changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: tableName }, (payload) => {
        // Update local state when DB changes
        setData((prev) => prev.map(item => item.id === payload.new.id ? payload.new : item));
      })
      .subscribe();

    return () => supabase.removeChannel(channel);
  }, [tableName]);

  return data;
};