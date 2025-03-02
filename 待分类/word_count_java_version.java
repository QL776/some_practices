public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
   Text k = new Text();
   IntWritable v = new IntWritable(1);

   @Override
   protected void map(LongWritable key, Text values, Context context) throws IOException, InterruptedException {
     String[] words = values.toString().split(" ");
     for(String word : words) {
        k.set(word);
        context.write(k,v);
     }
   }
}

public class WordCountReducer extends Reducer<LongWritable, Text, Text, IntWritable> {
    in sum;
    IntWritable v = new IntWritable();

    @Override
    protected void reducer(LongWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
      sum = 0;
      for(IntWritable count : values){
        sum += count.get();
      }
      v.set(sum);
      context.write(k,v);
    }
}
