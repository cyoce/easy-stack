class Program
  SEPARATORS = /[#{Regexp.escape(',.{}[]()')}]/
  @@functions = {}
  def initialize debug=0
    @stack = []
    @main = ['']
    @blocks = [@main]
    @debug = debug
    @functions = @@functions
  end
  
  attr_reader :stack
  
  def new_func name, arity=nil, &block
    @table[name] ||= -> do
      out = yield(*pop(arity || block.arity))
      push out if out
      nil
    end
  end
  
  def pop(n=nil)
    return stack.pop unless n
    stack.slice! -n, stack.size-n
  end
  
  def push(*args)
    stack.push(*args)
  end
  
  def active_block
    @stacks[-1]
  end
  
  def run text
    string = false
    text.chars do |c|
      if c == '"'
        if string
          active_block[-1] << ?"
          active_block << ''
          string = false
        else
          active_block << '"'
          string = true
        end
        next
      end
      
      if string
        active_block[-1] << c
        next
      end
      
      if /\s/ =~ c
        active_block << ''
      end
      
      if Program::SEPARATORS =~ c
        if c == ?{
          @stacks << ['']
          next
        elsif c == ?}
          closed = @blocks.pop
          active_block << Block.new(closed) << "'"
          next
        end
      end
      
     if active_block[-1] == ''
       vals = active_block.slice!(0, active_block.size-1)
       execute *vals
     end
    end
  end
  
  def execute *tokens
    tokens.each do |token|
      case token
      when Block
        push token
      when /"([^"]*)"/
        push $1
      when /-?[0-9]+/
        push token.to_i
      when /-?[0-9]*\.[0-9]+/
        push token.to_f
      when String
        cmd = @table.fetch(token){ raise "Unrecognized command: #{token.inspect}" }
        instance_exec &cmd
      end   
    end
  end
end   
Program.new()


class Block
  attr_reader :vals
  
  def initialize vals
    @vals = vals
  end
  
  def inspect
    @vals.map{|x| x.is_a?(Block) ? x.inspect : x}.reject!(&:empty?).join(' ')
  end
end









 










 











