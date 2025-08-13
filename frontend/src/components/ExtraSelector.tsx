import type { Extra } from '../types';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';

interface ExtraSelectorProps {
  extras: Extra[];
  selectedExtras: Extra[];
  onExtrasChange: (extras: Extra[]) => void;
}

const ExtraSelector = ({ extras, selectedExtras, onExtrasChange }: ExtraSelectorProps) => {
  const handleExtraToggle = (extra: Extra) => {
    const isSelected = selectedExtras.some(selected => selected.id === extra.id);
    
    if (isSelected) {
      onExtrasChange(selectedExtras.filter(selected => selected.id !== extra.id));
    } else {
      onExtrasChange([...selectedExtras, extra]);
    }
  };

  const calculateTotalPrice = () => {
    return selectedExtras.reduce((sum, extra) => sum + parseFloat(extra.price), 0).toFixed(2);
  };

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-semibold">Customize Your Order</h3>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-3">
          {extras.map((extra) => {
            const isSelected = selectedExtras.some(selected => selected.id === extra.id);
            
            return (
              <label
                key={extra.id}
                className={`flex items-center space-x-2 p-3 rounded-lg border-2 cursor-pointer transition-colors flex-shrink-0 ${
                  isSelected 
                    ? 'border-primary bg-primary/5' 
                    : 'border-border hover:border-border/50'
                }`}
              >
                <Checkbox
                  checked={isSelected}
                  onCheckedChange={() => handleExtraToggle(extra)}
                />
                <div className="flex gap-4">
                  <span>{extra.name}</span>
                  <span className="text-primary font-semibold">+€{extra.price}</span>
                </div>
              </label>
            );
          })}
        </div>
        
        {selectedExtras.length > 0 && (
          <div className="mt-4 p-3 bg-muted rounded-lg">
            <div className="flex justify-between items-center">
              <span className="font-medium">Extras Total:</span>
              <span className="text-lg font-bold text-primary">€{calculateTotalPrice()}</span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ExtraSelector;
