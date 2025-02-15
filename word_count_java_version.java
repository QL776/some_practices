public class WordCountMapper extends Mapper<LongWriteable, Text, Text, IntWriteable> {
   Text k = new Text();
   IntWriteable v = new IntWriteable(1);

   @Override
   protected void map(LongWriteable key, Text value, Context context) throws IOException, InterruptedException {
     String line = value.toString();
     String[] words = line.split(" ");

     for(String word : words) {
        k.set(word);
        context.write(k,v);
     }
   }
}

public class WordCountReducer extends Reducer<LongWriteable, Text, Text, IntWriteable> {
    in sum;
    IntWriteable v = new IntWriteable();

    @Override
    protected void reducer(LongWriteable key, Iterable<IntWriteable> values, Context context) throws IOException, InterruptedException {
      sum = 0;
      for(IntWriteable count : values){
        sum += count.get();
      }
      v.set(sum);
      context.write(k,v);
    }
}
