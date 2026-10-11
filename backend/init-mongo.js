// MongoDB Initialization Script
// Runs automatically when MongoDB container starts for the first time

// Switch to the application database
db = db.getSiblingDB('messmate_dev');

// Create collections with validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['email', 'full_name', 'role', 'password_hash'],
      properties: {
        email: { bsonType: 'string', pattern: '^.+@.+$' },
        full_name: { bsonType: 'string', minLength: 1, maxLength: 100 },
        role: { enum: ['student', 'admin', 'super_admin'] },
        password_hash: { bsonType: 'string' },
        active_session_id: { bsonType: 'string' },
        institution_id: { bsonType: 'string' },
        is_verified: { bsonType: 'bool' },
        is_blocked: { bsonType: 'bool' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('institutions', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'code'],
      properties: {
        name: { bsonType: 'string', minLength: 1, maxLength: 200 },
        code: { bsonType: 'string', minLength: 2, maxLength: 20 },
        address: { bsonType: 'string' },
        contact_email: { bsonType: 'string' },
        contact_phone: { bsonType: 'string' },
        is_active: { bsonType: 'bool' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('meal_rsvps', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'date', 'meal_type', 'opted_in'],
      properties: {
        user_id: { bsonType: 'string' },
        date: { bsonType: 'date' },
        meal_type: { enum: ['breakfast', 'lunch', 'snacks', 'dinner'] },
        opted_in: { bsonType: 'bool' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('wastage_records', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['date', 'meal_type', 'cooked_kg', 'wasted_kg'],
      properties: {
        date: { bsonType: 'date' },
        meal_type: { enum: ['breakfast', 'lunch', 'snacks', 'dinner'] },
        cooked_kg: { bsonType: 'double', minimum: 0 },
        wasted_kg: { bsonType: 'double', minimum: 0 },
        cost_per_kg: { bsonType: 'double', minimum: 0 },
        notes: { bsonType: 'string' },
        recorded_by: { bsonType: 'string' },
        created_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('menus', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['date', 'meal_type', 'items'],
      properties: {
        date: { bsonType: 'date' },
        meal_type: { enum: ['breakfast', 'lunch', 'snacks', 'dinner'] },
        items: {
          bsonType: 'array',
          items: {
            bsonType: 'object',
            required: ['name', 'category'],
            properties: {
              name: { bsonType: 'string' },
              category: { enum: ['veg', 'non_veg', 'special'] },
              description: { bsonType: 'string' }
            }
          }
        },
        created_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('notifications', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['title', 'body', 'target_audience'],
      properties: {
        title: { bsonType: 'string', maxLength: 100 },
        body: { bsonType: 'string', maxLength: 500 },
        target_audience: { enum: ['all', 'students', 'admins', 'specific'] },
        target_user_ids: { bsonType: 'array', items: { bsonType: 'string' } },
        sent_by: { bsonType: 'string' },
        sent_at: { bsonType: 'date' },
        read_by: { bsonType: 'array', items: { bsonType: 'string' } }
      }
    }
  }
});

db.createCollection('payment_transactions', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'amount', 'currency', 'status', 'razorpay_order_id'],
      properties: {
        user_id: { bsonType: 'string' },
        amount: { bsonType: 'double', minimum: 0 },
        currency: { bsonType: 'string', enum: ['INR'] },
        status: { enum: ['created', 'paid', 'failed', 'refunded'] },
        razorpay_order_id: { bsonType: 'string' },
        razorpay_payment_id: { bsonType: 'string' },
        razorpay_signature: { bsonType: 'string' },
        purpose: { enum: ['mess_fee', 'subscription', 'other'] },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('subscriptions', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'plan_id', 'status', 'current_period_start', 'current_period_end'],
      properties: {
        user_id: { bsonType: 'string' },
        plan_id: { bsonType: 'string' },
        status: { enum: ['active', 'cancelled', 'past_due', 'trialing'] },
        current_period_start: { bsonType: 'date' },
        current_period_end: { bsonType: 'date' },
        cancel_at_period_end: { bsonType: 'bool' },
        razorpay_subscription_id: { bsonType: 'string' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

// Create indexes for performance
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ institution_id: 1, role: 1 });
db.users.createIndex({ active_session_id: 1 });

db.meal_rsvps.createIndex({ user_id: 1, date: 1, meal_type: 1 }, { unique: true });
db.meal_rsvps.createIndex({ date: 1, meal_type: 1, opted_in: 1 });

db.wastage_records.createIndex({ date: 1, meal_type: 1 });
db.menus.createIndex({ date: 1, meal_type: 1 }, { unique: true });
db.notifications.createIndex({ sent_at: -1 });
db.payment_transactions.createIndex({ user_id: 1, created_at: -1 });
db.subscriptions.createIndex({ user_id: 1, status: 1 });

print('MongoDB initialization complete!');