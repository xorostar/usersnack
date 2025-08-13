import { useState } from 'react';
import type { CustomerInfo } from '../types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';

interface CustomerInfoFormProps {
  onSubmit: (customerInfo: CustomerInfo) => void;
  loading?: boolean;
}

const CustomerInfoForm = ({ onSubmit, loading = false }: CustomerInfoFormProps) => {
  const [formData, setFormData] = useState<CustomerInfo>({
    name: '',
    address: '',
  });

  const [errors, setErrors] = useState<Partial<CustomerInfo>>({});

  const handleInputChange = (field: keyof CustomerInfo, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<CustomerInfo> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.address.trim()) {
      newErrors.address = 'Address is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">
          Full Name *
        </Label>
        <Input
          type="text"
          id="name"
          value={formData.name}
          onChange={(e) => handleInputChange('name', e.target.value)}
          className={errors.name ? 'border-destructive' : ''}
          placeholder="Enter your full name"
        />
        {errors.name && (
          <p className="text-sm text-destructive">{errors.name}</p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="address">
          Delivery Address *
        </Label>
        <Textarea
          id="address"
          value={formData.address}
          onChange={(e) => handleInputChange('address', e.target.value)}
          rows={3}
          className={errors.address ? 'border-destructive' : ''}
          placeholder="Enter your delivery address"
        />
        {errors.address && (
          <p className="text-sm text-destructive">{errors.address}</p>
        )}
      </div>

      <Button
        type="submit"
        disabled={loading}
        className="w-full"
      >
        {loading ? 'Placing Order...' : 'Place Order'}
      </Button>
    </form>
  );
};

export default CustomerInfoForm;
